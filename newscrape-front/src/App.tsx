import ArticleList from "./components/ArticleList"
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import * as React from 'react';

export default function App(){
  return(
    <div>
      <React.Fragment>
        <CssBaseline />
        <Container maxWidth="sm">
          <Typography variant="h1" gutterBottom>
            Newscrape
          </Typography>
          <ArticleList />
        </Container>
      </React.Fragment>
    </div>
    
  )
}