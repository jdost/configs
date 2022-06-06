module Passwords (
    getPasswords
  , passwordPrompt
  ) where

import Control.Monad (forM)
import System.Directory (doesDirectoryExist, getDirectoryContents)
import System.FilePath ((</>))
import System.FilePath.Posix (dropExtension, makeRelative)
import System.Environment (getEnv, lookupEnv)
import Data.List (isInfixOf)
import Data.Maybe (fromMaybe)

import XMonad.Core
import XMonad.Prompt

passwordStoreEnvVar :: String
passwordStoreEnvVar = "PASSWORD_STORE_DIR"

passwordLength :: Int
passwordLength = 24

getFiles :: FilePath -> IO [String]
getFiles dir = do
  names <- getDirectoryContents dir
  let properNames = filter (`notElem` [ ".", "..", ".git" ]) names
  paths <- forM properNames $ \name -> do
    let path = dir </> name
    isDirectory <- doesDirectoryExist path
    if isDirectory
      then getFiles path
      else return [path]
  return (concat paths)

getPasswords :: IO [String]
getPasswords = do
  password_dir <- getPasswordDir
  files <- getFiles password_dir
  return $ map ((makeRelative password_dir) . dropExtension) files

getPasswordDir :: IO FilePath
getPasswordDir = do
  envDir <- lookupEnv passwordStoreEnvVar
  home <- getEnv "HOME"
  return $ fromMaybe (home </> ".password_store") envDir

data Pass = Pass

instance XPrompt Pass where
  showXPrompt       Pass = "Pass: "
  commandToComplete  _ c = c
  nextCompletion       _ = getNextCompletion

selectPassword :: [String] -> String -> X ()
selectPassword passwords ps = spawn $ "pass " ++ args
  where
    args | ps `elem` passwords = "show -c " ++ ps
         | otherwise = "generate -c " ++ ps ++ " " ++ (show passwordLength)

passwordPrompt :: XPConfig -> X ()
passwordPrompt config = do
  li <- io getPasswords
  let compl = \s -> filter (\x -> s `isInfixOf` x) li
  mkXPrompt Pass config (return . compl) (selectPassword li)
