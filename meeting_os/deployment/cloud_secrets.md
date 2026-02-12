# Cloud Deployment Checklist ☁️

## 1. Supabase (Database)
You need to create a project on [supabase.com](https://supabase.com) and get these details:
- [ ] **Host**: `db.xyz.supabase.co`
- [ ] **User**: `postgres`
- [ ] **Password**: (The one you set when creating the project)
- [ ] **Database**: `postgres` (default)
- [ ] **Port**: `5432` OR `6543` (Transaction Pooler - recommended for serverless)

## 2. Render (n8n Hosting)
When creating the 'Blueprint' in Render, it will ask for `supabase-creds`. You must provide:
- [ ] `HOST`: (from above)
- [ ] `USER`: (from above)
- [ ] `PASSWORD`: (from above)

Atomic Environment Variables to add manually if not in `render.yaml`:
- [ ] `N8N_ENCRYPTION_KEY`: Generate a random string (e.g., `openssl rand -hex 24`).
- [ ] `N8N_BASIC_AUTH_USER`: `admin`
- [ ] `N8N_BASIC_AUTH_PASSWORD`: `secure_password`

## 3. API Keys (For n8n Credentials)
Once n8n is running, you will need to add these **Credentials** inside the n8n UI:
- [ ] **Google Gemini API**: `{{GOOGLE_API_KEY}}`
- [ ] **Perplexity API**: `{{PERPLEXITY_API_KEY}}`
- [ ] **Linear API**: `{{LINEAR_API_KEY}}`
- [ ] **Notion API**: `{{NOTION_SECRET}}`

## 4. Vercel (Optional Frontend)
*Currently, we have no frontend code.* If you want to deploy a dashboard later:
- [ ] `NEXT_PUBLIC_SUPABASE_URL`
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY`
