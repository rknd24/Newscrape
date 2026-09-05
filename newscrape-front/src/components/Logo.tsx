import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'

// 3本の線が右にいくほど短くなる = 記事を要約で削ぎ落とすイメージ
function LogoMark() {
    return (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <line x1="4" y1="7" x2="20" y2="7" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="4" y1="12" x2="15" y2="12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="4" y1="17" x2="10" y2="17" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
        </svg>
    )
}

export default function Logo() {
    return (
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 3, color: "text.primary" }}>
            <LogoMark />
            <Typography
                component="h1"
                sx={{ fontWeight: 700, fontSize: { xs: 24, sm: 34 } }}
            >
                Newscrape
            </Typography>
        </Box>
    )
}
