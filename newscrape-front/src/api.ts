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

export function getNews(category: string, q?: string): Promise<Article[]> {
    const url = q ? `/news/${category}?q=${encodeURIComponent(q)}` : `/news/${category}`
    return fetch(url)
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
    return fetch(`/analyze`, {
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
