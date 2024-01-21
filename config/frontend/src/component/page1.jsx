import { Link } from "react-router-dom";
import { useParams } from 'react-router-dom';
import axios from 'axios';
import React, {useState, useEffect} from 'react';

export const Page1 = () => {
  //ステート設定
  const [detailJson, setdetailJson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  //post_idをパラメータから取得
  const { id } = useParams();
    
    //axios初回のみ起動
    useEffect(() => {     
      axios.post('http://127.0.0.1:8000/test3/', {id})
      .then(response => {
          const responseData = response.data;
          console.log(responseData)
          //jsonデータ格納
          setdetailJson(responseData)
          setIsLoading(false);
      })
      .catch(error => {
          console.error(error);
          setIsLoading(false);
      });
    }, []);

    // データ取得中 ローディング状態の表示
  if (isLoading) {
      return <div>Loading...</div>; 
  } 
  return (
    <div>
      <h1>{detailJson.post_user}さんの詳細ページ</h1>
      <p>タイトル：{detailJson.post_title}</p>
      <p>タグ：{detailJson.post_tag}</p>
      <p>
        <Link to="/">search</Link>
      </p>
    </div>
  );
};