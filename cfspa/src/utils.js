function getParams(pagination, searchTxt) {
  const page =
    typeof pagination === "object" &&
    typeof pagination.page === "number" &&
    pagination.page > 1
      ? pagination.page
      : false;
  const ordering =
    typeof pagination === "object" &&
    typeof pagination.sortBy === "string" &&
    pagination.sortBy.length > 0
      ? pagination.sortBy
      : false;
  const descending =
    typeof pagination === "object" &&
    typeof pagination.descending === "boolean" &&
    pagination.descending
      ? "-"
      : "";

  const rowsPerPage =
    typeof pagination === "object" &&
    typeof pagination.rowsPerPage === "number" &&
    pagination.rowsPerPage > 0
      ? pagination.rowsPerPage
      : false;

  const search =
    typeof searchTxt === "string" && searchTxt.length > 0 ? searchTxt : false;

  const params = {};

  if (page) {
    params.page = page;
  }

  if (ordering) {
    params.ordering = descending + ordering;
  }

  if (search) {
    params.search = search;
  }
  if (rowsPerPage) {
    params.page_size = rowsPerPage;
  }
  return params;
}

export { getParams };
