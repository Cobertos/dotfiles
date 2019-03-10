let input = parseInt(sys.argv[2],10)
if(input < 0) {
    throw new Error("The passed value must be between 0 and 255");
}

//0-255 => 0-1 => ^ 2.2 => 0-255, gamma correctio for source engine
console.log( Math.floor(Math.pow(input/255, 2.2) * 255) );