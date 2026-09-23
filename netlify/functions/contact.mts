export default async (req: Request) => {
  if (req.method !== "POST") return new Response(JSON.stringify({error:"method_not_allowed"}),{status:405,headers:{"content-type":"application/json"}});
  let data: Record<string, unknown> = {};
  try { data = await req.json(); } catch { return new Response(JSON.stringify({error:"invalid_json"}),{status:400,headers:{"content-type":"application/json"}}); }
  if (data.company_website) return new Response(JSON.stringify({ok:true}),{status:200,headers:{"content-type":"application/json"}});
  const hasContact = Boolean(data.email || data.phone || data.name || data.fullName);
  if (!hasContact) return new Response(JSON.stringify({error:"missing_contact"}),{status:400,headers:{"content-type":"application/json"}});
  const webhook = Netlify.env.get("CONTACT_WEBHOOK_URL");
  if (!webhook) return new Response(JSON.stringify({configured:false,error:"contact_backend_not_connected"}),{status:503,headers:{"content-type":"application/json","cache-control":"no-store"}});
  const upstream = await fetch(webhook,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({source:"green-therapy-site",submittedAt:new Date().toISOString(),...data})});
  if (!upstream.ok) return new Response(JSON.stringify({error:"delivery_failed"}),{status:502,headers:{"content-type":"application/json"}});
  return new Response(JSON.stringify({ok:true}),{status:200,headers:{"content-type":"application/json","cache-control":"no-store"}});
};
export const config = { path: "/api/contact" };
