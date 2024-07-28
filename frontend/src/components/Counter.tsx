import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Counter: React.FC = () => {
  const [sessionId, setSessionId] = useState<string>('');
  const [counter, setCounter] = useState<number>(0);
  const [newCount, setNewCount] = useState<number | string>(0);

  useEffect(() => {
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
    fetchCounter(newSessionId);

    return () => {
      deleteSession(newSessionId);
    };
  }, []);

  const generateSessionId = (): string => {
    return Math.random().toString(36).substr(2, 9);
  };

  const fetchCounter = async (sessionId: string) => {
    try {
      const response = await axios.get(`/api/${sessionId}/counter/`);
      console.log('Fetch Counter Response:', response.data);
      if (response.data.length > 0) {
        setCounter(response.data[0].current_count);
      }
    } catch (error) {
      console.error('Error fetching counter:', error);
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await axios.delete(`/api/${sessionId}/`);
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  };

  const changeCount = async (amount: number) => {
    const endpoint = amount > 0 ? `/api/${sessionId}/counter/increase` : `/api/${sessionId}/counter/decrease`;
    try {
      const response = await axios.post(endpoint);
      console.log('Change Count Response:', response.data);
      setCounter(response.data.current_count);
    } catch (error) {
      console.error('Error updating count:', error);
    }
  };

  const insertCount = async () => {
    if (typeof newCount === 'number') {
      try {
        const response = await axios.post(`/api/${sessionId}/counter/insert?new_number=${newCount}`);
        setCounter(response.data.current_count);
      } catch (error) {
        console.error('Error updating count:', error);
      }
    } else {
      console.error('Invalid input: newCount must be a number');
    }
  };

  return (
    <div className="container">
      <h1>{counter}</h1>
      <div className="buttons">
        <button onClick={() => changeCount(1)}>Increase</button>
        <button onClick={() => changeCount(-1)}>Decrease</button>
      </div>
      <div className="insert">
        <input
          type="number"
          value={newCount}
          onChange={(e) => setNewCount(Number(e.target.value))}
          placeholder="Change number"
        />
        <button onClick={insertCount}>Set</button>
      </div>
    </div>
  );
};

export default Counter;
