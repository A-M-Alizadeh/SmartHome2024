import styled from "@emotion/styled";
import { NavLink } from "react-router-dom";

// export const StyledNavLink = styled(NavLink)`

//   color: #fff;
//   font-size: 1.2rem;
//   text-decoration: none;
// `;
export const StyledNavLink = styled(NavLink)(({ theme }) => ({
  color: "#000",
  textDecoration:'none',
  "&.active": {
    color: "#f5b869",
    transition:'all 0.5s ease'
  },
}));
