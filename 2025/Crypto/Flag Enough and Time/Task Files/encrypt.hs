import Data.Time
import Data.Char (ord, chr)
import Data.Bits (xor)
import System.IO (writeFile)
import Data.Time.Clock.POSIX (utcTimeToPOSIXSeconds)


funName :: String -> String -> String
funName emblem timestamp = zipWith xorDigits emblem (cycle timestamp)
  where
    xorDigits f t = chr (ord f `xor` ord t)


encrypt :: String -> IO ()
encrypt emblem = do
    currentTime <- getCurrentTime
    let watch = floor (utcTimeToPOSIXSeconds currentTime) :: Integer
    
    let clock = show watch
    
    let encryptedemblem = funName emblem clock
    
    let magicformat = formatTime defaultTimeLocale "%FT%T%QZ" currentTime
    
    let output = "Flag: " ++ encryptedemblem ++ "\nTime encrypted: " ++ magicformat
    writeFile "flag.txt" output
    putStrLn "flag encrypted and written to flag.txt"


main :: IO ()
main = do
    let emblem = "XXXXXXXXXXXXXXXXXXXX"
    encrypt emblem

