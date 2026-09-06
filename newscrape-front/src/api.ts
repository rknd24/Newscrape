export interface Article {
    id: number
    title: string
    link: string
    category: string
    summary: string | null
    fetched_at: string
}

export interface AnalyzeResponse {
    title: string
    report: string
}

// 本番はビルド時に VITE_API_BASE（Renderの https://xxx.onrender.com）を注入する。
// ローカルは空文字 → Vite の proxy が /news, /analyze を localhost:8000 に転送する。
const API_BASE = import.meta.env.VITE_API_BASE ?? ""

export function getNews(category: string, q?: string): Promise<Article[]> {
    const path = q
        ? `/news/${category}?q=${encodeURIComponent(q)}`
        : `/news/${category}`
    return fetch(API_BASE + path)
        .then(res => res.json().then(data => ({ ok: res.ok, data })))
        .then(({ ok, data }) => {
            if (ok) {
                return data.articles as Article[]
            } else {
                throw new Error("Failed to fetch articles")
            }
        })
}

export function analyze(article: Article): Promise<AnalyzeResponse> {
    return fetch(API_BASE + `/analyze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(article)
    }).then(res => res.json().then(data => ({ ok: res.ok, data })))
        .then(({ ok, data }) => {
            if (ok) {
                return data
            } else {
                throw new Error("Failed to analyze article")
            }
        })
}
