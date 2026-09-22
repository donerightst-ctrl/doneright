import { ToolLoopAgent, type Message, type ModelAdapter, type ModelTurn, createConstructionTools } from '../src/agent.js';

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(`Assertion failed: ${message}`);
}

class ScriptedModel implements ModelAdapter {
  private index = 0;
  constructor(private readonly turns: ModelTurn[]) {}
  async next(_messages: readonly Message[]): Promise<ModelTurn> {
    const turn = this.turns[this.index++];
    if (!turn) throw new Error('script exhausted');
    return turn;
  }
}

async function run(): Promise<void> {
  {
    const model = new ScriptedModel([
      { type: 'tool', call: { name: 'record_material_request', arguments: { item: 'cement', quantity: 20, unit: 'bags', site: 'A' } } },
      { type: 'final', text: 'Request captured for approval.' },
    ]);
    const result = await new ToolLoopAgent(model, createConstructionTools()).run('Need 20 bags of cement for site A');
    assert(result.text === 'Request captured for approval.', 'tool then final');
    assert(result.messages[3].content.includes('needs-human-approval'), 'approval state');
  }

  {
    const model = new ScriptedModel([
      { type: 'tool', call: { name: 'record_material_request', arguments: { item: 'cement', quantity: -1, unit: 'bags', site: 'A' } } },
      { type: 'final', text: 'Please provide a positive quantity.' },
    ]);
    const result = await new ToolLoopAgent(model, createConstructionTools()).run('Need cement');
    assert(result.messages[3].content.includes('positive quantity'), 'validation error returned to model');
  }

  {
    const model = new ScriptedModel([
      { type: 'tool', call: { name: 'delete_database', arguments: {} } },
      { type: 'final', text: 'That action is not available.' },
    ]);
    const result = await new ToolLoopAgent(model, createConstructionTools()).run('Delete everything');
    assert(result.messages[3].content.includes('Tool not allowed'), 'unknown tool blocked');
  }

  {
    const model = new ScriptedModel([
      { type: 'tool', call: { name: 'record_material_request', arguments: { item: 'steel', quantity: 1, unit: 'ton', site: 'B' } } },
    ]);
    let failed = false;
    try {
      await new ToolLoopAgent(model, createConstructionTools(), 1).run('Need steel');
    } catch (error) {
      failed = error instanceof Error && error.message.includes('exceeded maxSteps=1');
    }
    assert(failed, 'max-step fail closed');
  }

  console.log('4/4 tests passed');
}

void run();
