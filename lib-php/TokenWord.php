<?php

namespace Nominatim\Token;

/**
 * A standard word token.
 */
class Word
{
    /// Database word id, if applicable.
    public $iId;
    /// Number of appearances in the database.
    public $iSearchNameCount;
    /// Number of terms in the word.
    public $iTermCount;

    public function __construct($iId, $iSearchNameCount, $iTermCount)
    {
        $this->iId = $iId;
        $this->iSearchNameCount = $iSearchNameCount;
        $this->iTermCount = $iTermCount;
    }

    public function debugInfo()
    {
        return array(
                'ID' => $this->iId,
                'Type' => 'word',
                'Info' => array(
                           'count' => $this->iSearchNameCount,
                           'terms' => $this->iTermCount
                          )
               );
    }
}
