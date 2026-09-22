export type Role = 'system' | 'user' | 'assistant' | 'tool';

export interface Message {
  role: Role;
  content: string;
  name?: string;
}

export interface ToolCall {
  name: string;
  arguments: Record<string, unknown>;
}

export type ModelTurn =
  | { type: 'final'; text: string }
  | { type: 'tool'; call: ToolCall };

export interface ModelAdapter {
  next(messages: readonly Message[]): Promise<ModelTurn>;
}

export interface Tool {
  description: string;
  run(args: Record<string, unknown>): Promise<unknown>;
}

export interface AgentResult {
  text: string;
  steps: number;
  messages: Message[];
}

export class ToolLoopAgent {
  constructor(
    private readonly model: ModelAdapter,
    private readonly tools: Record<string, Tool>,
    private readonly maxSteps = 6,
  ) {
    if (!Number.isInteger(maxSteps) || maxSteps < 1) {
      throw new Error('maxSteps must be a positive integer');
    }
  }

  async run(userInput: string, systemPrompt = 'Be helpful and use tools only when needed.'): Promise<AgentResult> {
    const messages: Message[] = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userInput },
    ];

    for (let step = 1; step <= this.maxSteps; step += 1) {
      const turn = await this.model.next(messages);

      if (turn.type === 'final') {
        messages.push({ role: 'assistant', content: turn.text });
        return { text: turn.text, steps: step, messages };
      }

      const tool = this.tools[turn.call.name];
      if (!tool) {
        const available = Object.keys(this.tools).sort().join(', ') || '(none)';
        const error = `Tool not allowed: ${turn.call.name}. Available tools: ${available}`;
        messages.push({ role: 'assistant', content: JSON.stringify(turn.call) });
        messages.push({ role: 'tool', name: turn.call.name, content: JSON.stringify({ ok: false, error }) });
        continue;
      }

      messages.push({ role: 'assistant', content: JSON.stringify(turn.call) });

      try {
        const value = await tool.run(turn.call.arguments);
        messages.push({
          role: 'tool',
          name: turn.call.name,
          content: JSON.stringify({ ok: true, value }),
        });
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        messages.push({
          role: 'tool',
          name: turn.call.name,
          content: JSON.stringify({ ok: false, error: message }),
        });
      }
    }

    throw new Error(`Agent exceeded maxSteps=${this.maxSteps} without a final response`);
  }
}

export function createConstructionTools(): Record<string, Tool> {
  return {
    record_material_request: {
      description: 'Validate and normalize a construction material request before it is queued.',
      async run(args) {
        const item = String(args.item ?? '').trim();
        const quantity = Number(args.quantity);
        const unit = String(args.unit ?? '').trim();
        const site = String(args.site ?? '').trim();

        if (!item || !unit || !site || !Number.isFinite(quantity) || quantity <= 0) {
          throw new Error('item, positive quantity, unit, and site are required');
        }

        return {
          item,
          quantity,
          unit,
          site,
          status: 'needs-human-approval',
        };
      },
    },
  };
}
