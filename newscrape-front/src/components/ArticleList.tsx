import ArticleCard from "./ArticleCard"
import { useState, useEffect } from "react"
import Box from '@mui/material/Box'
import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import Search_Bar from "./SearchBar"
import { getNews, type Article } from "../api"
import ChatPanel from "./ChatPanel"

type Status = "idle" | "loading" | "success" | "error"

const CATEGORIES = [
    { value: "all", label: "総合" },
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
    const [category, setCategory] = useState("all")
    const [query, setQuery] = useState("")
    const [state, setState] = useState<Status>("idle")
    // AIパネルで深掘り中の記事。null ならパネルは閉じている
    const [focusedId, setFocusedId] = useState<number | null>(null)

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

    const focusedArticle = articleData.find(a => a.id === focusedId)

    return (
        <Box sx={{ display: "flex", gap: 3, alignItems: "flex-start" }}>
            {/* 左: 検索・カテゴリ・記事一覧 */}
            <Box sx={{ flex: 1, minWidth: 0 }}>
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
                            <ArticleCard
                                article={article}
                                key={article.link}
                                onAskAI={setFocusedId}
                            />
                        ))}
                    </Box>
                )}
            </Box>

            {/* 右: AIパネル。記事の「AIに聞く」で開く。その1記事に絞って深掘りする。
                別の記事を選ぶ or 閉じると focusedId が変わり、ChatPanel が作り直されて会話がリセットされる */}
            {focusedArticle && (
                <ChatPanel
                    key={focusedId}
                    article={focusedArticle}
                    onClose={() => setFocusedId(null)}
                />
            )}
        </Box>
    )
}
