import React from 'react'

export default function ImageShow({source,altText,size}) {
    return (
        
            <img src={source} alt={altText} className={`max-w-xs mx-auto ${size<24?'hidden md:flex':''} h-${size} w-${size}`} />
        
    )
}
