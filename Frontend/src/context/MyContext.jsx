import { createContext, useContext, useState } from "react"


export const MyContext = createContext();

const MyProvider = ({ children }) => {
    const [open, setOpen] = useState(true);


    return (
        <MyContext.Provider value={{ open, setOpen }}>
            {children}
        </MyContext.Provider>
    )

}

export default MyProvider;

export const MyAppContext = () =>  useContext(MyContext);
