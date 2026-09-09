import ArticleCard from "./ArticleCard"
import { useState, useEffect } from "react"
import Box from '@mui/material/Box'
import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import CloseIcon from '@mui/icons-material/Close'
import Search_Bar from "./SearchBar"
import { getNews, type Article } from "../api"
import Chat from "./Chat"

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
                別の記事を選ぶ or 閉じると focusedId が変わり、Chat が作り直されて会話がリセットされる */}
            <Box
                sx={{
                    display: focusedId !== null ? "flex" : "none",
                    // スマホは全画面固定、PCは横並びの sticky サイドバー
                    position: { xs: "fixed", md: "sticky" },
                    inset: { xs: 0, md: "auto" },
                    top: { md: 16 },
                    zIndex: { xs: 1200, md: "auto" },
                    width: { xs: "auto", md: 380 },
                    flexShrink: 0,
                    height: { xs: "100%", md: "calc(100vh - 32px)" },
                    bgcolor: "background.paper",
                    border: { md: 1 },
                    borderColor: "divider",
                    borderRadius: { md: 2 },
                    flexDirection: "column",
                    overflow: "hidden",
                }}
            >
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        gap: 1,
                        px: 2,
                        py: 1,
                        borderBottom: 1,
                        borderColor: "divider",
                    }}
                >
                    <Box sx={{ minWidth: 0 }}>
                        <Typography variant="caption" color="text.secondary">
                            この記事についてAIに質問
                        </Typography>
                        <Typography sx={{ fontWeight: 600, fontSize: 14 }} noWrap>
                            {focusedArticle?.title ?? ""}
                        </Typography>
                    </Box>
                    <IconButton onClick={() => setFocusedId(null)} size="small">
                        <CloseIcon />
                    </IconButton>
                </Box>

                <Box sx={{ flex: 1, minHeight: 0 }}>
                    {focusedId !== null && (
                        <Chat key={focusedId} articleId={focusedId} />
                    )}
                </Box>
            </Box>
        </Box>
    )
}
