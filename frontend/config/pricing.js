export const pricingTable = {
  "gpt-4": 0.06,             // $0.06 per 1K tokens
  "gpt-3.5": 0.002,          // $0.002 per 1K tokens
  "ollama:llama2": 0.0001,   // example cost for local model
  "ollama:mistral": 0.0001,  // local model
  "mixtral": 0.005           // sample public estimate
};

export function estimateCost(model, tokens) {
  const rate = pricingTable[model] || 0;
  return `$${((tokens / 1000) * rate).toFixed(4)}`;
}
