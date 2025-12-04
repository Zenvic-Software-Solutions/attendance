import {
    makeGetRequest,
    makePostRequest,
    makePatchRequest,
    makeDeleteRequest,
    makeCustomRequest,
    makeFromRequest,
    makePutRequest,
} from "./methods/makeRequest";

// // authApi
export const login = (data) => makePostRequest("access/admin/login/", data);
//User
export const getUserList = (page = 1, search) => makeGetRequest(`access/user/list/?page=${page}&search=${search}`);
export const getUserName = (page = 1) => makeGetRequest(`access/user/list/?page=${page}`);
export const getUserFilterName = () => makeGetRequest(`cms/user/meta/`);

// export const getUserList = (params) =>
//   makeGetRequest("access/user/list/", params);
export const getUserDetails = (uuid) => makeGetRequest(`access/user/retrieve/${uuid}/`);

//Task
export const getTaskList = (uuid, startDate, endDate, category, page) => makeGetRequest(`cms/task/list/?created_at__gte=${startDate}&created_at__lte=${endDate}&category=${category}&user=${uuid}&page=${page}`);
// export const getTaskList = (uuid, params = {}) => makeGetRequest(`cms/user/task/list/${uuid}/`, params);
export const getTaskDetails = (uuid) => makeGetRequest(`cms/user/task/retrieve/${uuid}/`);

//Update User Status
export const updateUserStatus = (uuid, payload) =>
    makePatchRequest(`access/user/cud/${uuid}/`, payload);



//Attendance
export const getAttendanceDetails = (uuid, date) => makeGetRequest(`cms/user/punch/list/${uuid}/?punch_date=${date}`);

// Work Category
export const addWorkCategory = (data) => makePostRequest("cms/category/", data);
export const getWorkCategory = (page = 1, search) => makeGetRequest(`cms/category/list/?page=${page}&search=${search}`);
export const getCategoryName = (page = 1) => makeGetRequest(`cms/category/list/?page=${page}`);


// export const getWorkCategory = (params) =>
//   makeGetRequest("cms/category/list/", params);

export const editWorkCategory = (id, data) => makePutRequest(`cms/category/${id}/`, data);

//Dashboard
export const getAttendanceDashboard = () => makeGetRequest("cms/dashboard/");

//Reports
// export const getUnpaidBookings = (startDate, endDate) =>
//   makeGetRequest(
//     `common/reports/unpaid-bookings/?from_date=${startDate}&to_date=${endDate}`
//   );
// export const getTransactionReport = (startDate, endDate) =>
//   makeGetRequest(
//     `common/reports/transactions/?from_date=${startDate}&to_date=${endDate}`
//   );
// export const getBookingsReport = (startDate, endDate) =>
//   makeGetRequest(common/`reports/bookings/?from_date=${startDate}&to_date=${endDate}`);

//Booking
// export const getBookingList = (page = 1, searchText) =>
//   makeGetRequest(`common/bookings/?page=${page}&search=${searchText}`);
// export const getBookings = (searchText) =>
//   makeGetRequest(`common/bookings/?search=${searchText}`);
// export const addBookingList = (data) => makePostRequest("common/bookings/", data);
// export const patchBookingList = (data, id) =>
//   makePutRequest(`common/bookings/${id}/`, data);
// export const deleteBookingList = (id) => makeDeleteRequest(`common/bookings/${id}/`);
// export const getBookingById = (id) => makeGetRequest(`common/bookings/${id}/`);
// export const getCustomers = () => makeGetRequest("common/customers/");
// export const getBookedTypes = () => makeGetRequest("common/travels/");
// export const addBookedType = (data) => makePostRequest("common/travels/", data);
// export const updateBookedType = (id, data) =>
//   makePutRequest(`common/travels/${id}/`, data);
// export const getTransactionById = (id) =>
//   makeGetRequest(`common/bookings/${id}/transactions/`);