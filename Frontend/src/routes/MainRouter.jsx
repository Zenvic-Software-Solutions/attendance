import { createBrowserRouter } from "react-router-dom";
import ErrorBoundary from "./ErrorBoundary";
import ProtectedRoute from "./ProtectedRoute";

import MainLayout from "@/layouts/MainLayout";
import { Dashboard, Login, UserList, UserDetail, Task, Attendance, WorkCategory, TaskDetail } from "@/pages";

const MainRouter = createBrowserRouter([
  {
    index: true,
    element: <Login />,
  },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    // errorElement: <ErrorBoundary />,
    children: [
      {
        path: "dashboard",
        element: <Dashboard/>,
      },
      {
        path: "user",
        children:[
          {path:"",element: <UserList />},
          {path:":uuid", element:<UserDetail />}
        ]
      },
     {
        path: "task",
        children:[
          {path:"",element: <Task />},
          {path:":uuid",element: <TaskDetail />},


        ]
       
      },
       {
        path: "task/:uuid",
        element: <Task />
      },

      {
        path:"attendance",
        element: <Attendance/>
      },
      
      {
        path: "work-category",
        element: <WorkCategory />
      },

  
      // {
      //   path: `userdetail/:uuid`,
      //   element: <UserDetail />,
      // },
      // {
      //   path: "booking",
      //   children: [
      //     { path: "list", element: <BookingList /> },
      //     { path: "add", element: <AddBooking /> }, // Add form
      //     { path: "edit/:id", element: <AddBooking /> }, // Edit form
      //     { path: "view/:id", element: <Invoice /> }, // View mode (readonly)
      //     { path: "transactions/:id", element: <TransactionList /> }, // Transaction view
      //   ],
      // },
    
      // {
      //   path: "customer",
      //   children: [
      //     { path: "detail/:uuid", element: <CustomerDetail /> },
      //     { path: "list", element: <CustomerList /> },
      //   ],
      // },
      {
        path: "*",
        element: <div>404 - Page Not Found</div>,
      },
      // { path: "test", element: <Test /> },
    ],
  },
]);

export default MainRouter;
