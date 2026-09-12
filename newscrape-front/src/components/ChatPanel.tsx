import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import CloseIcon from '@mui/icons-material/Close'
import Chat from './Chat'
import type { Article } from '../api'

type Props = {
    article: Article
    onClose: () => void
}

// AIパネルの枠（位置・ヘッダー・閉じるボタン）だけを持つ。会話そのものは Chat の仕事。
export default function ChatPanel({ article, onClose }: Props) {
    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
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
                        {article.title}
                    </Typography>
                </Box>
                <IconButton onClick={onClose} size="small">
                    <CloseIcon />
                </IconButton>
            </Box>

            <Box sx={{ flex: 1, minHeight: 0 }}>
                <Chat articleId={article.id} />
            </Box>
        </Box>
    )
}
