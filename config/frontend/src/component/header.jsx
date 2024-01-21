import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "../static/css/style.css";


const Header = () => {
  //ステータス設定
  const [is_authenticated, setIs_authenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSituationMenu, setIsSituationMenu] = useState(false);
  

  //フック設定 フォームの値が更新されるごとにfetchDataを実行
  useEffect(() => {
    fetchData();
  }, []);

  // JSONデータの取得と設定を行う非同期関数
  const fetchData = async () => { 
    console.log('確認する１')
    axios.get('http://127.0.0.1:8000/header/')
    .then(response => {
        const responseData = response.data;
        console.log('session')
        console.log(responseData)
        //jsonデータ格納
        setIs_authenticated(responseData)
        setIsLoading(false);
    })
    .catch(error => {
        console.error(error);
        setIsLoading(false);
    });
  }

  const headerMenu = () =>{
    setIsSituationMenu(!isSituationMenu)
  };

  const iStyle = {
    marginLeft: '-10px',
    marginRight: '10px',
  };  
    //const displayedItems = searchJson.slice(0, itemCount);
    //style="margin-left:-10px;margin-right:10px" 一旦コメントアウト
  // データ取得中 ローディング状態の表示
  if (true) {
    return <header>
              <div>
                <ul className="header-munu-ul">
                  <div className="flex">
                    {/* SforHロゴ */} 
                    <div className="cover1">
                      <a><img className="logo" src={`${process.env.PUBLIC_URL}/logo_transparent.png`} alt="SforHロゴ" ></img></a>
                    </div> 
                  </div>
                    {/* ユーザーコンテンツ */}
                    <li onClick={headerMenu} className="nav_item"><a href="#"><small className='nav-text'>kawase keita</small></a>
                      <div>
                        {isSituationMenu &&  (
                          <ul style={{ transition: 'height 0.5', overflow: 'hidden'}}>
                          <li class="panel_item"><a href="">Logout</a></li>
                          <li class="panel_item"><a href="">Change Password</a></li>
                          <li class="panel_item"><a href="">投稿する</a></li>
                          </ul>
                        )}
                      </div>
                    </li>
                </ul>
              </div>
           </header>
  } else {
    return <div>ログアウト中</div>
  }
    
};

export default Header;