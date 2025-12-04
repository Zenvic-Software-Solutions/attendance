import { RouterProvider } from 'react-router-dom'
import { Toaster } from "react-hot-toast";
import './App.css'
import MainRouter from './routes/MainRouter'

function App() {

  return (
    <>
     <RouterProvider router={MainRouter} />
     <Toaster position="top-center" reverseOrder={false} />
    </>
  )
}

export default App
