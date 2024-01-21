import React, { useState } from 'react';

const SearchForm = (onSearch) => {

    const [searchTitle, setSearchTitle] = useState({
        // フォームの各フィールドに対応する初期値をここで設定
        title: '',
        // 他のフィールドも同様に設定
      });

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setSearchTitle((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      };

    const handleSearchClick = () => {
        const title = searchTitle.title
        onSearch(title);
    };

    return(
        <>
            <input 
            type="text"
            name="title"
            value={searchTitle.title}
            onChange={handleInputChange}
            />
            <button onClick={handleSearchClick}>検索</button>
        </>
    );
}

export default SearchForm;
