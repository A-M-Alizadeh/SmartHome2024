import styled from "@emotion/styled";
import { Typography } from "@mui/material";

export const StyledText = styled(Typography)`
  /* color: #f5b869; */
  color: ${(props) => (props.variant === "textTitle" ? " #f5b869" : "#fff")};
  font-size: ${(props) =>
    props.variant === "textTitle" ? "1.1rem" : "0.9rem"};
  cursor: ${(props) => (props.variant === "link" ? "pointer" : "default")};
`;
