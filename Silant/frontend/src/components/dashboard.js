import React, { useState, useEffect, Fragment } from 'react';

const Dashboard = () => {
  const [userUsername, setUserUsername] = useState('');
  const [loading, setLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('token') === null) {
      setIsAuth(false)
    } else {
      fetch('http://127.0.0.1:8002/api/auth/user/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(data => {
          console.log(data)
          setUserUsername(data.userUsername);
          setLoading(false);
          setIsAuth(true)
        });
    }
  }, []);

  return (
    <div>
      {loading === false && (
        <Fragment>
          <h1>Dashboard</h1>
          <h2>Hello {userUsername}!</h2>
        </Fragment>
      )}
    </div>
  );
};

export default Dashboard;