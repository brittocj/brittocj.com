import { onRequest } from '../functions/api/views.js';

interface Env {
  KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname !== '/api/views') {
      return new Response('Not found', { status: 404 });
    }

    return onRequest({ request, env } as Parameters<typeof onRequest>[0]);
  },
};
