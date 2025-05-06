import { getSession } from 'next-auth/react';
import { Configuration, OpenAIApi } from 'openai';
import { Anthropic } from '@anthropic-ai/sdk';

export default async function handler(req, res) {
  const session = await getSession({ req });
  if (!session) return res.status(401).end();
  const { provider } = req.query;
  if (provider === 'openai') {
    const client = new OpenAIApi(new Configuration({ apiKey: session.user.openaiKey }));
    const data = await client.listModels();
    return res.json(data.data.map(m => m.id));
  }
  if (provider === 'anthropic') {
    const client = new Anthropic({ apiKey: session.user.anthropicKey });
    const data = await client.listModels();
    return res.json(data.models.map(m => m.name));
  }
  res.status(400).json({ error: 'Provider invalide' });
}