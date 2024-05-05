import { styled } from "styled-components";

export const StyledInput = styled.input`
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 3px;
  width: 90%;
  height: 50px;
  background-color: transparent;
  padding-left: 10px;
  color: #fff;
  font-size: 1.2rem;
  outline: none;
  &::placeholder {
    color: #b3b3b3;
  }

  &:focus {
    outline: none;
    box-shadow: 1px 1px 3px 2px rgba(255, 255, 255, 0.5);
    transition: all 0.5s ease;
  }
`;
