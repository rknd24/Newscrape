import ArticleCard from "./ArticleCard"

const newArray = Array(4).fill({title:"article"})

export default function ArticleList(){
    return(
        newArray.map((article,index)=>
        <ArticleCard title={article.title} key={index} />
    )
)
}
