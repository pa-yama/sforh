//import { Link } from "react-router-dom";
import { useParams } from 'react-router-dom';
import axios from 'axios';
import React, { useState, useEffect } from 'react';
import "../static/css/style.css";
import config from '../config';

import CreatePostEditButton from './createPostEditButton';

export const Detail = () => {
  //ステート設定
  const [detailJson, setdetailJson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const [text_comment, setText_comment] = useState(null);
  const [text_comment_ReplyToReply, setText_comment_ReplyToReply] = useState(null);



  //post_idをパラメータから取得
  const { id } = useParams();
  const { user_id } = '1';


  //画面表示数設定 初期値2
  const [commentCount, setCommentCount] = useState(1);

  //もっと表示
  const hendleShowMore = () => {
    setCommentCount(prevCommentCount => prevCommentCount + 1)
  }

  const indicationReplyZone = (comment_id) => {
    console.log(comment_id)
    //返信ゾーンを表示する。

    document.getElementById('replyZone_' + comment_id).style.display = 'block';

  };


  // JSONデータの取得と設定を行う非同期関数
  //いいねの処理
  const goodPost = async () => {
    console.log('いいねする投稿idを確認')
    console.log(detailJson.post_id)
    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/goodPost/')
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData)
        setIsLoading(false);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }
  // JSONデータの取得と設定を行う非同期関数
  //いいね解除の処理
  const unlikePost = async () => {
    console.log('いいね解除する投稿idを確認')
    console.log(detailJson.post_id)

    //リアクションIDをdjango側に渡す必要がある。

    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/unlikePost/', { reaction_id: detailJson.reaction_id })
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData);
        setIsLoading(false);
        //setisAlreadyGood(detailJson.isAlreadyGood);
        //setReaction_id(detailJson.reaction_id);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }

  // JSONデータの取得と設定を行う非同期関数
  //コメントにいいねの処理
  const goodComment = async (comment_id) => {
    console.log('いいね解除するコメントidを確認')
    console.log(detailJson.post_id)
    //alert(comment_id)

    //リアクションIDをdjango側に渡す必要がある。

    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/goodComment/', { comment_id: comment_id })
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData);
        setIsLoading(false);
        //setisAlreadyGood(detailJson.isAlreadyGood);
        //setReaction_id(detailJson.reaction_id);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }

  // JSONデータの取得と設定を行う非同期関数
  //コメントにいいね解除の処理
  const unLikeComment = async (reaction_id) => {
    console.log('いいね解除するコメントidを確認')
    console.log(detailJson.post_id)
    //alert(reaction_id)

    //リアクションIDをdjango側に渡す必要がある。

    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/unlikeComment/', { comment_id: reaction_id })
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData);
        setIsLoading(false);
        //setisAlreadyGood(detailJson.isAlreadyGood);
        //setReaction_id(detailJson.reaction_id);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }












  // JSONデータの取得と設定を行う非同期関数
  //コメント投稿の処理
  const sendComment = async () => {
    console.log('コメント内容の確認')
    console.log(text_comment)
    console.log('投稿IDの確認')
    console.log(detailJson.post_id)

    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/comment/', { text_comment: text_comment, lastComment_id: detailJson.lastComment_id })
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData)
        setIsLoading(false);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }

  // JSONデータの取得と設定を行う非同期関数
  //コメント返信の処理
  const sendReply = async (comment_id) => {
    console.log('コメント内容の確認')
    console.log(text_comment)
    console.log('投稿IDの確認')
    console.log(detailJson.post_id)
    //alert(comment_id)
    //alert(text_comment)

    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/reply/', { text_comment: text_comment, comment_id: comment_id })
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData)
        setIsLoading(false);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }

  // JSONデータの取得と設定を行う非同期関数
  //返信コメントに返信の処理
  const sendReplyToReply = async (comment_id) => {
    console.log('コメント内容の確認')
    console.log(text_comment)
    console.log('投稿IDの確認')
    console.log(detailJson.post_id)
    //alert(comment_id)
    //alert(text_comment)

    axios.post('http://127.0.0.1:8000/detail/' + detailJson.post_id + '/replyToReply/', { text_comment: text_comment_ReplyToReply, comment_id: comment_id })
      .then(response => {
        const responseData = response.data;
        console.log('確認する２')
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData)
        setIsLoading(false);
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }



  //axios初回のみ起動
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/detail/' + id + '/', { user_id })
      .then(response => {
        const responseData = response.data;
        console.log(responseData)
        //jsonデータ格納
        setdetailJson(responseData)
        console.log(detailJson)
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
    <div className='detail-html'>
      <p>投稿者:{detailJson.name}</p>
      <h2>タイトル</h2>
      <div>
        <input
          type="text"
          name="タイトル"
          placeholder={detailJson.title}
          class="text-title">
        </input>
      </div>
      <h2>内容</h2>
      <div>
        <textarea
          type="text"
          name="タイトル"
          placeholder={detailJson.text_probrem}
          class="text-content">
        </textarea>
      </div>
      <div>
        <p>タグ:{detailJson.tag}</p>
      </div>
      <div>
        <p>編集可能フラグ:{detailJson.isActiveEdit}</p>
      </div>
      {detailJson.isActiveEdit === 'True' && (
        <div>
          <CreatePostEditButton post_id={detailJson.post_id}></CreatePostEditButton>
        </div>
      )}
      <div>
        <p>コメント数:{detailJson.commentCount}</p>
      </div>
      <p>---------------------------------</p>
      <p>いいねボタン</p>
      <p>いいねフラグ:{detailJson.isAlreadyGood}</p>

      <p>いいね数 : {detailJson.reactionCount}</p>

      <p>最終コメントID : {detailJson.lastComment_id}</p>

      {detailJson.isAlreadyGood === 'True' && (
        <button onClick={unlikePost}>いいね解除a</button>
      )}
      {detailJson.isAlreadyGood === 'False' && (
        <button onClick={goodPost}>いいねa</button>
      )}

      <p>---------------------------------</p>
      <p>コメントを投稿する。</p>
          <div>コメント内容</div>
          <div>
            <input
              type="text"
              name="text_comment"
              onChange={(event) => setText_comment(event.target.value)}
              class="text-comment"
            />
          </div>
        <div class="show-space">
            <button 
            class="show-more"
            onClick={sendComment}>送信</button>
        </div>


      <p>---------------------------------</p>
      <p>コメントの表示</p>
      {detailJson.commentListdictionaries.map((comment, index) => {
        if (index < commentCount) {
          return <div key={index} className='comment-item'>
            <p>★★★★★★★★★★★★★★★★★★★★★★★★</p>
            <p>{comment.comment_id}</p>
            <p>{comment.text_comment}</p>
            <p>リアクションID{comment.reaction_id}</p>

            <p>いいね数 : {comment.count}</p>
            <p>既にいいねしてるか : {comment.isAlreadyGood}</p>

            {comment.isAlreadyGood === 'True' && (
              <button onClick={() => { unLikeComment(comment.reaction_id) }}>いいね解除b</button>
            )}
            {comment.isAlreadyGood === 'False' && (
              <button onClick={() => { goodComment(comment.comment_id) }}>いいねb</button>
            )}

            <p>返信の有無 : {comment.haveReply}</p>


            {comment.haveReply === 'True' && (
              <p style={{ color: 'red' }} onClick={() => { indicationReplyZone(comment.comment_id) }}>返信を表示する</p>
            )}

            <div id={"replyZone_" + comment.comment_id} style={{ display: 'none' }}>

              <p>最終返信コメントID : {comment.lastReplyComment_id}</p>
              {comment.commentReplyListdictionaries.map((reply, index2) => {
                return <div key={index2} className='reply-item'>
                  <p>-----------返信開始------------</p>
                  <p>{reply.comment_id}</p>
                  <p>{reply.text_comment}</p>
                  <p>いいね数 : {reply.count}</p>

                  {reply.isAlreadyGood === 'True' && (
                    <button onClick={() => { unLikeComment(reply.reaction_id) }}>いいね解除b</button>
                  )}
                  {reply.isAlreadyGood === 'False' && (
                    <button onClick={() => { goodComment(reply.comment_id) }}>いいねb</button>
                  )}


                  {comment.lastReplyComment_id === reply.comment_id && (
                    <div>
                      <p>最終コメントです</p>
                      <p>返信コメントに返信する</p>
                      <table>
                        <tr>
                          <td>コメント内容</td>
                          <td>
                            <input
                              type="text"
                              name="text_comment_ReplyToReply"
                              onChange={(event) => setText_comment_ReplyToReply(event.target.value)}
                            />
                          </td>
                        </tr>
                        <tr>
                          <td>
                            <button onClick={() => { sendReplyToReply(reply.comment_id) }}>送信</button>
                          </td>
                        </tr>
                      </table>
                    </div>
                  )}

                  <p>-----------返信終了------------</p>
                </div>
              })}
            </div>

            {comment.isAlreadyGood === 'False' && (
              <div>
                <p>コメントに返信する</p>
                <table>
                  <tr>
                    <td>コメント内容</td>
                    <td>
                      <input
                        type="text"
                        name="text_comment"
                        onChange={(event) => setText_comment(event.target.value)}
                      />
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <button
                        onClick={() => { sendReply(comment.comment_id) }}>
                        送信
                      </button>
                    </td>
                  </tr>
                </table>
              </div>
            )}


            <p>★★★★★★★★★★★★★★★★★★★★★★★★</p>
          </div>
        }
      })}

      {/* 
        {searchJson.map((item, index) => {
          if (index <= itemCount){      
            return <div key={index}>
              <p>{item.title}</p>
              <p>{item.tag}</p>
              <p>post_id={item.post_id}</p>
              <DetailButton post_id={item.post_id}></DetailButton>
          </div>
          }  
          })}
      */}
      <div class="show-space">
      <button 
      class="show-more"
      onClick={hendleShowMore}>show more...
      </button >
      </div>
    </div>
  );
};

export default Detail;