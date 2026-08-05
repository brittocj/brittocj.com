const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const SLUG_PATTERN = /^[a-z0-9-]+$/;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS,
    },
  });
}

async function readCount(env, slug) {
  const value = await env.KV.get(slug);
  return parseInt(value || '0', 10);
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS_HEADERS });
  }

  if (!env.KV) {
    return json({ error: 'Views storage is not configured.' }, 503);
  }

  const url = new URL(request.url);

  if (request.method === 'GET') {
    const slug = url.searchParams.get('slug');
    const slugsParam = url.searchParams.get('slugs');

    if (slugsParam) {
      const slugs = slugsParam.split(',').filter((item) => SLUG_PATTERN.test(item));
      const counts = {};

      await Promise.all(
        slugs.map(async (item) => {
          counts[item] = await readCount(env, item);
        })
      );

      return json({ counts });
    }

    if (slug && SLUG_PATTERN.test(slug)) {
      return json({ slug, count: await readCount(env, slug) });
    }

    return json({ error: 'Missing or invalid slug.' }, 400);
  }

  if (request.method === 'POST') {
    let payload;

    try {
      payload = await request.json();
    } catch {
      return json({ error: 'Invalid JSON body.' }, 400);
    }

    const slug = payload?.slug;

    if (!slug || !SLUG_PATTERN.test(slug)) {
      return json({ error: 'Missing or invalid slug.' }, 400);
    }

    const count = (await readCount(env, slug)) + 1;
    await env.KV.put(slug, String(count));

    return json({ slug, count });
  }

  return json({ error: 'Method not allowed.' }, 405);
}
