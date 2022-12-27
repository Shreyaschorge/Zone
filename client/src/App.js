import './App.css';
import axios from 'axios'
import {useState, useEffect} from 'react'

function App() {

  const [resp, setResp] = useState(null)

  const fetchProduct = async () => {
    try {
      const res = await axios.get('/api/payments');
      setResp(res.data)
      console.log(res.data)
    } catch (err) {
      console.log(err)
    }
  }

  useEffect(() => {
    fetchProduct();
  }, [])

  return (
    <div className="App">
      <h2>Hello World {resp}</h2>
    </div>
  );
}

export default App;
