import { createTheme } from '@mui/material/styles'

// OS標準のフォントをそのまま使う。Mac/iOSはヒラギノ角ゴシック+San Francisco、
// WindowsはYu Gothic/Meiryoにフォールバックする。Roboto固定にしない。
const theme = createTheme({
    typography: {
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Hiragino Kaku Gothic Pro"',
            '"Hiragino Sans"',
            '"Yu Gothic Medium"',
            'Meiryo',
            'sans-serif',
        ].join(','),
    },
})

export default theme
