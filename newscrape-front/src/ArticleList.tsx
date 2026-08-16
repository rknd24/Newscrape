import ArticleCard from "./ArticleCard.tsx"

const newsArray = Array(5).fill({title:"title"})


export default function ArticleList() {
    return(
        newsArray.map((article,index) => (
            <ArticleCard title={article.title} key={index} />
        ))
    )
    
}
