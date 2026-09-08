import ArticleCard from "./ArticleCard"
import { useState, useEffect } from "react"
import Box from '@mui/material/Box'
import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import Fab from '@mui/material/Fab'
import IconButton from '@mui/material/IconButton'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'
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
    const [chatOpen, setChatOpen] = useState(false)

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
                            <ArticleCard article={article} key={article.link} />
                        ))}
                    </Box>
                )}
            </Box>

            {/* 右: AIチャット。開いているときだけ横に居座る（背景は暗くしない）。
                閉じても display:none にするだけでアンマウントしない = 会話を保持 */}
            <Box
                sx={{
                    display: chatOpen ? "flex" : "none",
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
                        px: 2,
                        py: 1,
                        borderBottom: 1,
                        borderColor: "divider",
                    }}
                >
                    <Typography sx={{ fontWeight: 600 }}>AIに質問</Typography>
                    <IconButton onClick={() => setChatOpen(false)} size="small">
                        <CloseIcon />
                    </IconButton>
                </Box>

                <Box sx={{ flex: 1, minHeight: 0 }}>
                    <Chat articles_ids={articleData.map(a => a.id)} />
                </Box>
            </Box>

            {/* 開くボタン。パネルが閉じているときだけ表示 */}
            {!chatOpen && (
                <Fab
                    color="primary"
                    variant="extended"
                    onClick={() => setChatOpen(true)}
                    sx={{ position: "fixed", bottom: 24, right: 24 }}
                >
                    <AutoAwesomeIcon sx={{ mr: 1 }} />
                    AIに質問
                </Fab>
            )}
        </Box>
    )
}
