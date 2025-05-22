export const pricingTable = {
  "gpt-4": { input: 0.03, output: 0.06 },          // OpenAI gpt-4
  "gpt-3.5": { input: 0.0015, output: 0.002 },     // OpenAI gpt-3.5
  "ollama:llama2": { input: 0.00005, output: 0.0001 },  // local model sample
  "ollama:mistral": { input: 0.00005, output: 0.0001 }, // local model sample
  "mixtral": { input: 0.002, output: 0.005 }       // estimated Mixtral
};

export function estimateCost(model, inputTokens = 0, outputTokens = 0) {
  const pricing = pricingTable[model];
  if (!pricing) return "$0.0000";
  const inputCost = (inputTokens / 1000) * (pricing.input || 0);
  const outputCost = (outputTokens / 1000) * (pricing.output || 0);
  return `$${(inputCost + outputCost).toFixed(4)}`;
}
