import React, { useState, useEffect, useRef } from "react";

interface ContainerProps {
  children: React.ReactNode;
}

function Conteiner({ children }: ContainerProps) {
  const ref = useRef(null);
  const [isOverflowing, setIsOverflowing] = useState(false);

  useEffect(() => {
    if (ref.current.scrollHeight > ref.current.clientHeight) {
      setIsOverflowing(true);
    }
  }, [children]);

  return (
    <div
      ref={ref}
      className={`my-8 px-28 
       ${
         isOverflowing
           ? "min-h-screen"
           : "h-[89vh] flex justify-center items-center"
       }
      `}
    >
      {children}
    </div>
  );
}

export default Conteiner;
