import React, { useState } from "react";
import ArrowCircleLeftIcon from "@mui/icons-material/ArrowCircleLeft";
import ArrowCircleRightIcon from "@mui/icons-material/ArrowCircleRight";
import ExpandCircleDownIcon from '@mui/icons-material/ExpandCircleDown';

import "./carousel.css";

export const Carousel = ({ data }) => {

const [slide, setSlide] = useState(0);
console.log(data.length -1)

const nextSlide = () => {
    setSlide(slide === data.length -1 ? 0 : slide + 1)
}

const prevSlide = () => {
    setSlide(slide === 0 ? data.length -1 : slide - 1)
}
  return (
    <div className="carousel">
      <ArrowCircleLeftIcon className="arrow arrow-left" onClick={prevSlide} />
      {data.map((item, index) => {
        return (
          <img
            src={item.src}
            key={index}
            alt={`${item.alt}_index`}
            className={slide === index ? "slide": "slide slide-hidden"}
          />
        );
      })}
      <ArrowCircleRightIcon className="arrow arrow-right" onClick={nextSlide}/>
      <span className="indicators">
        {data.map((_, index) => {
          return (
            <button key={index} onClick={() => {setSlide(index)}} className={slide == index ? "indicator" : "indicator indicator-inactive"}></button>
          );
        })}
      </span>
    </div>
  );
};
