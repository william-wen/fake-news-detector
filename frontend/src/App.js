import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import Form from './components/Form/Form';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>The current time is {currentTime}.</p>
        <Form />
      </header>
    </div>
  );
}

export default App;
