import React from "react";
import { IoIosRefreshCircle } from "react-icons/io";

interface LoadingProps {
	isLoading: boolean;
	className?: string;
	divHeight?: string;
}
function Loading({ isLoading, className, divHeight }: LoadingProps) {
	if (!isLoading) {
		return null;
	}

	return (
		<div className={`flex justify-center items-center ${divHeight}`}>
			<IoIosRefreshCircle
				className={`animate-spin min-h-[2rem] min-w-[2rem] ${className}`}
			/>
		</div>
	);
}

export default Loading;
