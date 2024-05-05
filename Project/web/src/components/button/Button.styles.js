import styled from "@emotion/styled";

export const StyledButton = styled.button`
  background-color: #0070E0;
  color: #fff;
  text-transform: ${(props)=>props.variant === 'register' ? 'uppercase': 'capitalize'};
  width: 100%;
  height: 40px;
  border-radius: ${(props)=> props.variant ==='radius' ? '3px' : '0px' };
  outline: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.5s ease-out;
  &:hover {
  /* background-color: ${(props)=> (props.variant === 'radius') ? ' #474790' : '#fff'};
  color: ${(props)=> props.variant === 'radius' ? ' #fff' : '#000'}; */
  background-color: ${(props)=>props.buttons ==="buttons" ? "#004d99" : "#fff"};
  color: ${(props)=> props.buttons === 'buttons' ?"#fff" : "#000"}; 
  }
`;

// background-color: #353455;