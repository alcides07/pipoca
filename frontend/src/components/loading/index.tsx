import React from "react";
import { IoIosRefreshCircle } from "react-icons/io";

interface LoadingProps {
  isLoading: boolean;
  className?: string;
}
function Loading({ isLoading, className }: LoadingProps) {
  if (!isLoading) {
    return null;
  }

  return (
    <div className="flex justify-center items-center">
      <IoIosRefreshCircle
        className={`animate-spin text-white min-h-[2rem] min-w-[2rem] ${className}`}
      />
    </div>
  );
}

export default Loading;
