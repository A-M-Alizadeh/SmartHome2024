import styled from "@emotion/styled";
import {Link} from 'react-router-dom'
export const StyledLink = styled(Link)`
  color:#4da6ff;
  text-decoration:none;
  transition: all 0.5s ease-out;
  cursor: pointer;
  &:hover {
  color: ${(props)=> props.variant === 'linkhover' ? ' #fff' : '#000'};
  }
`;