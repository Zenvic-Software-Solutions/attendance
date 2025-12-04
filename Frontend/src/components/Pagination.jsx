import { Pagination as MuiPagination, Stack } from "@mui/material";
import React from "react";

const Pagination = ({
    currentPage,
    totalPages,
    onPageChange,
    maxVisiblePages = 2,
}) => {
    const handlePrev = () => {
        if (currentPage > 1) onPageChange(currentPage - 1);
    };

    const handleNext = () => {
        if (currentPage < totalPages) onPageChange(currentPage + 1);
    };

    const getPageNumbers = () => {
        const pages = [];

        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = startPage + maxVisiblePages - 1;

        if (endPage > totalPages) {
            endPage = totalPages;
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            pages.push(i);
        }

        return pages;
    };

    return (
        <Stack spacing={2} alignItems="flex-end" mt={2}>
            <MuiPagination
                count={totalPages}               
                page={currentPage}               
                onChange={(e, value) => onPageChange(value)} 
                siblingCount={Math.floor(maxVisiblePages / 2)} 
                boundaryCount={1}                
                variant="outlined"              
                shape="rounded"                 
                color="primary"
            />
        </Stack>
    );
};

export default Pagination;
