// import { useAppContext } from "@/context/Context";
// import qs from "qs";
import { normalInstance, accessInstance, handleError } from "./axiosInstance";

export const makeGetRequest = async (endpoint, params = {}, auth = true) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const formattedParams = {};
    Object.keys(params).forEach((key) => {
      const value = params[key];

      if (
        value !== null &&
        value !== undefined &&
        value !== "" &&
        (!Array.isArray(value) || value.length > 0)
      ) {
        formattedParams[key] = Array.isArray(value) ? value.join(",") : value;
      }
    });

       // Serialize params using qs for cleaner URLs
    // const queryString = qs.stringify(formattedParams, {
    //   skipNulls: true,
    //   addQueryPrefix: true, // Adds "?" automatically
    // });

    // const fullUrl = `${endpoint}${queryString}`;
    // const { data } = await instance.get(fullUrl);

    const { data } = await instance.get(endpoint, {
      params: formattedParams,
    });

    return data.data;
  } catch (error) {
    handleError(error);
  }
};

export const makePostRequest = async (endpoint, body, auth = true) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const { data } = await instance.post(endpoint, body);
    return data.data;
  } catch (error) {
    handleError(error);
  }
};

export const makePutRequest = async (endpoint, body, auth = true) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const { data } = await instance.put(endpoint, body);
    return data.data;
  } catch (error) {
    handleError(error);
  }
};

export const makePatchRequest = async (endpoint, body, auth = true) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const { data } = await instance.patch(endpoint, body);
    return data.data;
  } catch (error) {
    handleError(error);
  }
};

export const makeDeleteRequest = async (endpoint, body, auth = true) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const { data } = await instance.delete(endpoint, body);
    return data.data;
  } catch (error) {
    handleError(error);
  }
};

export const makeCustomRequest = async (
  endpoint,
  method = "GET",
  body = {},
  headers = {},
  responseType = "json",
  auth = true
) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const config = {
      method: method,
      url: endpoint,
      headers: {
        ...headers,
      },
      responseType: responseType,
      ...(method !== "GET" && { data: body }),
    };

    const { data } = await instance(config);
    return data;
  } catch (error) {
    handleError(error);
  }
};

export const makeFromRequest = async (
  endpoint,
  method = "GET",
  formData = null,
  auth = true
) => {
  const instance = auth ? normalInstance : accessInstance;
  try {
    const config = {
      method: method,
      url: endpoint,
      headers: {
        "Content-Type": "multipart/form-data",
      },
      data: formData,
      responseType: "json",
    };

    const { data } = await instance(config);
    return data;
  } catch (error) {
    handleError(error);
  }
};

// export const makeProgressRequest = async (
//   endpoint,
//   method = "GET",
//   body = {},
//   headers = {},
//   responseType = "json",
//   auth = true
// ) => {
//   const { setUploadProgress } = useAppContext();
//   const instance = auth ? normalInstance : accessInstance;

//   try {
//     const config = {
//       method: method,
//       url: endpoint,
//       headers: {
//         ...headers,
//       },
//       onUploadProgress: (progressEvent) => {
//         const progress = Math.round(
//           (progressEvent.loaded * 100) / progressEvent.total
//         );
//         setUploadProgress((prev) => [...prev, progress]);
//       },
//       responseType: responseType,
//       ...(method !== "GET" && { data: body }),
//     };

//     const { data } = await instance(config);
//     setUploadProgress(0);
//     return data;
//   } catch (error) {
//     setUploadProgress(0);
//     handleError(error);
//   }
// };
