import ArticleCard from "./ArticleCard"
import { useState, useEffect } from "react"
import Box from '@mui/material/Box'
import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import Search_Bar from "./SearchBar"
import { getNews, type Article } from "../api"

type Status = "idle" | "loading" | "success" | "error"

const CATEGORIES = [
    { value: "top-picks", label: "総合" },
    { value: "domestic", label: "国内" },
    { value: "world", label: "国際" },
    { value: "business", label: "経済" },
    { value: "entertainment", label: "エンタメ" },
    { value: "sports", label: "スポーツ" },
    { value: "it", label: "IT" },
    { value: "science", label: "科学" },
    { value: "local", label: "地域" },
]

export default function ArticleList() {
    const [articleData, setArticleData] = useState<Article[]>([])
    const [category, setCategory] = useState("top-picks")
    const [query, setQuery] = useState("")
    const [state, setState] = useState<Status>("idle")

    const loadNews = () => {
        setState("loading")
        getNews(category, query)
            .then(articles => {
                setArticleData(articles)
                setState("success")
            })
            .catch(() => setState("error"))
    }

    useEffect(() => {
        loadNews()
    }, [category, query])

    return (
        <Box>
            <Box sx={{ mb: 2, maxWidth: 400 }}>
                <Search_Bar onSearch={setQuery} />
            </Box>

            <Tabs
                value={category}
                onChange={(_, v) => setCategory(v)}
                variant="scrollable"
                scrollButtons="auto"
                sx={{ mb: 3, borderBottom: 1, borderColor: "divider" }}
            >
                {CATEGORIES.map(c => (
                    <Tab key={c.value} label={c.label} value={c.value} />
                ))}
            </Tabs>

            {state === "loading" && <Typography sx={{ my: 2 }}>読み込み中…</Typography>}

            {state === "error" && (
                <Box sx={{ my: 2 }}>
                    <Typography>読み込みに失敗しました。</Typography>
                    <Button onClick={loadNews}>再読み込み</Button>
                </Box>
            )}

            {state === "success" && (
                <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2 }}>
                    {articleData.map(article => (
                        <ArticleCard article={article} key={article.link} />
                    ))}
                </Box>
            )}
        </Box>
    )
}
