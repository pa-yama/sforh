import { Link } from "react-router-dom";
import { useParams } from 'react-router-dom';
import axios from 'axios';
import React, {useState, useEffect} from 'react';
import "../static/css/style.css";
import config from '../config';

export const CreatePost = () => {
  //ステート設定
  const [createPostJson, setCreatePostJson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  //const [createPostTitle, setCreatePostTitle] = useState(null);
  //const [createPostTag, setCreatePostTag] = useState(null);
  //const [createPostProblem, setCreatePostProblem] = useState(null);

  const { id } = useParams();

  const [createPostValue, setCreatePostValue] = useState({
    title: '',
    tag: '',
    problem: '',
  });




  const [initial_values, setInitial_values] = useState({
    post_id: '',
    user: '',
    title: '',
    tag: '',
    problem: '',
  });


  //フォーム値変更時動作
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setCreatePostValue((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  /*
  //検索時動作
  const handleSearchClick = () => {
    const title = createPostValue.title
    const tag = createPostValue.tag
    const problem = createPostValue.plobrem
    console.log(title)
    setCreatePostTitle(title);
    setCreatePostTag(tag);
    setCreatePostProblem(problem);
  };
  */

  //投稿作成の処理
  const createPost = async () => {    

    const pathname = window.location.pathname;
    let url = '';

    //pathnameに「edit」が含まれている場合、
    if(pathname.includes('edit')) {
      //詳細画面から来た場合
      url = 'http://127.0.0.1:8000/createPost/edit/' + id + '/create/';
    } else if(pathname.includes('tmpEdit')) {
      //一時保存中リストから来た場合
      url = 'http://127.0.0.1:8000/createPost/tmpEdit/' + id + '/create/';
    } else {
      //headerから来た場合
      url = 'http://127.0.0.1:8000/createPost/create/';
    }



    console.log('投稿idを確認')
    console.log(createPostJson.post_id)
    //axios.post('http://127.0.0.1:8000/createPost/create/', { title: createPostValue.title, tag: createPostValue.tag, problem: createPostValue.problem})
    axios.post(url, {title: createPostValue.title, tag: createPostValue.tag, problem: createPostValue.problem})
    .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        //setCreatePostJson(responseData)
        //setIsLoading(false);
    })
    .catch(error => {
        console.error(error);
        setIsLoading(false);
    });
  }


  //一時保存の処理
  const savePost = async () => {    
    console.log('いいねする投稿idを確認')
    console.log(createPostJson.post_id)
    
    const pathname = window.location.pathname;
    let url = '';

    //pathnameに「edit」が含まれている場合、
    if(pathname.includes('edit')) {
      //詳細画面から来た場合
      url = 'http://127.0.0.1:8000/createPost/edit/' + id + '/save/';
    } else if(pathname.includes('tmpEdit')) {
      //一時保存中リストから来た場合
      url = 'http://127.0.0.1:8000/createPost/tmpEdit/' + id + '/save/';
    } else {
      //headerから来た場合
      url = 'http://127.0.0.1:8000/createPost/save/';
    }


    axios.post(url, { title: createPostValue.title, tag: createPostValue.tag, problem: createPostValue.problem})
    .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        //setCreatePostJson(responseData)
        //setIsLoading(false);
    })
    .catch(error => {
        console.error(error);
        setIsLoading(false);
    });
  }
  
    
  //axios初回のみ起動
  useEffect(() => {     
    //alert(prev.prevScreenName)

    const pathname = window.location.pathname;
    let url = '';

    //pathnameに「edit」が含まれている場合、
    if(pathname.includes('edit')) {
      //詳細画面から来た場合
      url = 'http://127.0.0.1:8000/createPost/edit/' + id + '/';
    } else if(pathname.includes('tmpEdit')) {
      //一時保存中リストから来た場合
      url = 'http://127.0.0.1:8000/createPost/tmpEdit/' + id + '/';
    } else {
      //headerから来た場合
      url = 'http://127.0.0.1:8000/createPost/';
    }


    
    


    


    


    //alert(url)

    axios.get(url)
    .then(response => {
        const responseData = response.data;
        console.log(responseData)
        //jsonデータ格納
        setCreatePostJson(responseData)
        console.log(createPostJson)
        setIsLoading(false);
        console.log(responseData.initial_values);

        //setCreatePostValue(createPostJson.initial_values);

        if (responseData.initial_values != null) {
          //初期値がある場合は埋める処理を追記する。
          //console.log(createPostJson.initial_values);
          //alert(createPostJson.initial_values.title);
          
          if(//responseData.initial_values.post_id !== 'undefind' &&
          //responseData.initial_values.user !== 'undefind'  && 
          responseData.initial_values.title != 'undefind'  && 
          responseData.initial_values.tag != 'undefind'  && 
          responseData.initial_values.problem != 'undefind') {
            //initial_valuesが存在する場合は初期値をセットする。
            setCreatePostValue(responseData.initial_values);
          }

           
        }
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

      <p>投稿作成画面</p>

      <p>遷移前の画面</p>
      {/*
        <p>{prevScreenName}</p>
      */}

      <p>タイトル</p>
      <input className='input-area'
                      type="text"
                      name="title"
                      value={createPostValue.title}
                      onChange={handleInputChange}
      />

      <p>タグ</p>
      <input className='input-area'
                      type="text"
                      name="tag"
                      value={createPostValue.tag}
                      onChange={handleInputChange}
      />

      <p>問題</p>
      <input className='input-area'
                      type="text"
                      name="problem"
                      value={createPostValue.problem}
                      onChange={handleInputChange}
      />

      <p></p>
      <input hidden name='postId' value="投稿ID"></input>
      <p></p>
      <input type='submit' name='submit' value='投稿' onClick={createPost}></input>
      <p></p>
      <input type='submit' name='submit' value='一時保存' onClick={savePost}></input>

    </div>
  );
};

export default CreatePost;