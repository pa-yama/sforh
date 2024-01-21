import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
//import DetailButton from './detailButton';
import "../static/css/style.css";
import config from '../config';

const SearchPost = () => {
  //ステータス設定
  const [searchJson, setSearchJson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTitle, setSearchTitle] = useState(null);
  const [searchTag, setSearchTag] = useState(null);
  //フォームを変更する度に値を更新
  const [searchValue, setSearchValue] = useState({
    title: '',
    tag: '',
  });
  //画面表示数設定 初期値10
  const [itemCount, setItemCount] = useState(2);


  //フック設定 フォームの値が更新されるごとにfetchDataを実行
  useEffect(() => {
    fetchData();
  }, [searchTitle,searchTag]);

  //フォーム値変更時動作
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setSearchValue((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  //検索時動作
  const handleSearchClick = () => {
    const title = searchValue.title
    const tag = searchValue.tag
    console.log(title)
    setSearchTitle(title);
    setSearchTag(tag);
  };

  //もっと表示
  const hendleShowMore = () => {
    setItemCount(prevItemCount => prevItemCount + 1)
    console.log('確認');
    console.log(searchJson.tag);
  }

    // JSONデータの取得と設定を行う非同期関数
    const fetchData = async () => {
      if(searchTitle == null){
        setSearchTitle('')
      }
      axios.post(config.apiUrl + 'searchPost/', {searchTitle,searchTag})
      .then(response => {
          const responseData = response.data;
          console.log('レスポンスデータ')
          console.log(responseData)
          //jsonデータ格納
          setSearchJson(responseData)
          setIsLoading(false);  
      })
      .catch(error => {
          console.error(error);
          setIsLoading(false);
      });
    }

    const tagSearch = (tagItem) =>{
      setSearchTag(tagItem);
    }

    const navigate = useNavigate();

    const detailPage = (post_id) =>{
      
      //navigate('/page1/' + props.post_id);
      navigate('/detail/' + post_id);
  };
    //const displayedItems = searchJson.slice(0, itemCount);

  // データ取得中 ローディング状態の表示
  if (isLoading) {
    return <div>Loading...</div>;
  }
    return <div className='search-html'>
              <table>
                <tr>
                  <td>
                    <input className='title-text'
                      type="text"
                      name="title"
                      value={searchValue.title}
                      onChange={handleInputChange}
                      />
                  </td>
                {/* タグ検索を削除
                <tr>
                <td>タグ</td>
                  <td>
                      <input 
                      type="text"
                      name="tag"
                      value={searchValue.tag}
                      onChange={handleInputChange}
                      />
                  </td>
                </tr>
                */}
                  <td>
                      <button onClick={handleSearchClick}>検索</button>
                  </td>
                </tr>
              </table>
              {searchJson.map((item, index) => {
                if (index <= itemCount){
                  const tags = item.tag.split(',');
                  console.log(tags);
                  return <div key={index} className='search-item'>
                    <div onClick={() => detailPage(item.post_id)}>
                    <p>{item.username}</p>
                    <p className='title-item'>{item.title}</p>
                    </div>
                    <p className='tag-space'>
                      <span>{item.insert_timestamp}</span>
                       {/*<span className='detail-button'><DetailButton post_id={item.post_id}></DetailButton></span>*/}
                      {/* タグをカンマ区切りで表示 */}
                      {tags.map((tag, tagIndex) => (
                        <span className='tag-item' key={tagIndex} onClick={() => tagSearch(tag.trim())}>{tag.trim()}</span>
                      ))}
                    </p>
                </div>
                }
                })}
              <div className='show-space'>
                <button className='show-more'  onClick={hendleShowMore}>show-more</button >
              </div>
            </div>
};

export default SearchPost;