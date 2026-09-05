// ISO形式の日時文字列を「3時間前」のような相対表記に変換する
export function formatRelativeTime(isoString: string): string {
    const diffMs = Date.now() - new Date(isoString).getTime()
    const diffMin = Math.floor(diffMs / 1000 / 60)

    if (diffMin < 1) return "たった今"
    if (diffMin < 60) return `${diffMin}分前`

    const diffHour = Math.floor(diffMin / 60)
    if (diffHour < 24) return `${diffHour}時間前`

    const diffDay = Math.floor(diffHour / 24)
    return `${diffDay}日前`
}
