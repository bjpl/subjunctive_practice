/**
 * Typed selector hook
 */

import { TypedUseSelectorHook, useSelector } from 'react-redux';
import type { RootState } from '../types/api';

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
