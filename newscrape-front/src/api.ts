export interface Article{
        title: string,
        link : string
}

export interface AnalyzeResponse{
    title: string,
    report: string
}

export function getNews(category:string): Promise<Article[]>{
    return fetch(`/news/${category}`)
        .then(res => res.json().then(data => ({ok:res.ok,data})))
        .then(({ok,data}) => {
            if(ok){
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
    }).then(res => res.json().then(data => ({ok:res.ok,data})))
    .then(({ok,data}) => {
        if(ok){
            return data
        } else {
            throw new Error("Failed to analyze article")
        }
    })
}