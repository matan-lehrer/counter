import React, { useState, useEffect } from 'react';

const Counter: React.FC = () => {
    const [count, setCount] = useState<number>(0);
    const [newCount, setNewCount] = useState<number | string>(0);
    const sessionId = 1;

    useEffect(() => {
        fetchCount();
    }, []);

    const fetchCount = async () => {
        try {
            const response = await fetch(`/api/${sessionId}/counter/`);
            const data = await response.json();
            const latestCount = data.length > 0 ? data[0].current_count : 0;
            setCount(latestCount);
        } catch (error) {
            console.error('Error fetching count:', error);
        }
    };

    const changeCount = async (amount: number) => {
        const endpoint = amount > 0 ? `/api/${sessionId}/counter/increase` : `/api/${sessionId}/counter/decrease`;
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            setCount(data.current_count);
        } catch (error) {
            console.error('Error updating count:', error);
        }
    };

    const insertCount = async () => {
        if (typeof newCount === 'number') {
            try {
                const response = await fetch(`/api/${sessionId}/counter/insert?new_number=${newCount}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                setCount(data.current_count);
            } catch (error) {
                console.error('Error updating count:', error);
            }
        } else {
            console.error('Invalid input: newCount must be a number');
        }
    };

    return (
        <div className="container">
            <h1>{count}</h1>
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
